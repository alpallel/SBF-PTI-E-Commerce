from rest_framework import serializers
from .models import User, Category, Items, Cart, CartItem


class UserSerializer(serializers.ModelSerializer):
    user_password = serializers.CharField(write_only=True, required=False)
    user_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ("user_id", "username", "user_password", "user_picture", "created_at")
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.user_password = validated_data.get("user_password", instance.user_password)
        instance.user_picture = validated_data.get("user_picture", instance.user_picture)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ItemsSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(read_only=True)
    item_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Items
        fields = ("item_id", "item_name", "item_description", "item_picture", "item_category", "price", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemsSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all(), source="item", write_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "item", "item_id", "quantity")
        read_only_fields = ("id", "item")

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.item = validated_data.get("item", instance.item)

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    cart_items = CartItemSerializer(many=True, source="cart_items", required=False)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "cart_items", "total_price")

    def create(self, validated_data):
        cart_items_data = validated_data.pop("cart_items", [])
        user = validated_data.pop("user")
        cart = Cart.objects.create(user=user)
        for ci in cart_items_data:
            item = ci.get("item")
            quantity = ci.get("quantity", 1)
            CartItem.objects.create(cart=cart, item=item, quantity=quantity)
        return cart

    def update(self, instance, validated_data):
        user = validated_data.get("user")
        if user is not None:
            instance.user = user
            instance.save()

        incoming = {ci["item"].id: ci for ci in validated_data.get("cart_items", [])}
        existing_qs = instance.cart_items.select_related("item").all()
        existing_ids = {ci.item.id for ci in existing_qs}

        # update or create
        for item_id, ci in incoming.items():
            obj, created = CartItem.objects.update_or_create(
                cart=instance, item_id=item_id,
                defaults={"quantity": ci.get("quantity", 1)}
            )

        # remove items not present in incoming
        to_remove = [ci for ci in existing_qs if ci.item.id not in incoming]
        for ci in to_remove:
            ci.delete()

        return instance
