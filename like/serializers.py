from rest_framework import serializers
from .models import Like, Favorite

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    owner_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        post = attrs['post']
        if user.likes.filter(post=post).exists():
            raise serializers.ValidationError(
                'You have already liked this post!'
            )
        return attrs
    
class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    owner_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post_title'] = instance.post.title
        if instance.post.preview:
            preview = instance.post.preview
            representation['post_preview'] = preview.url
        else:
            representation['post_preview'] = None
        return representation
        