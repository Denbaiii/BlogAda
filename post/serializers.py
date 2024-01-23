from rest_framework import serializers
from post.models import Post, PostImages
from category.models import Category
from like.serializers import LikeSerializer
from comment.serializers import CommentSerializer

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source = 'category.name')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['quantity of likes'] = 0
        for _ in representation['likes']:
            representation['quantity of likes'] += 1
        return representation

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category', 'category_name', 'preview', 'owner_username')


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(
        required = True, queryset = Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ('title', 'body', 'preview', 'category','images')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            PostImages.objects.create(images=image, post=post)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()
    
    @staticmethod
    def is_favorite(post, user):
        return user.favorites.filter(post=post).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['quantity of likes'] = 0
        for _ in representation['likes']:
            representation['quantity of likes'] += 1
        user = self.context['request'].user
        representation['comment'] = CommentSerializer(instance.comments.all(), many = True).data
        representation['comments_count'] = instance.comments.count()
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance, user)
            representation['is_favorite'] = self.is_favorite(instance, user)
        return representation