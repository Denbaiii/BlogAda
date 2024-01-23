from rest_framework import serializers
from .models import Comment
from post.models import Post

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Comment
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
    
class CommentActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')
    post = serializers.CharField(required = False)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        post = self.context.get('post')
        post = Post.objects.get(pk = post)
        validated_data['post'] = post
        owner = self.context.get('owner')
        validated_data['owner'] = owner
        return super().create(validated_data)