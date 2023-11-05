from rest_framework import serializers
# from api.models import Post
class PostSerializers(serializers.ModelSerializer):
    class Meta:
        # model = Post  
        # exclude = ['is_removed', 'created', 'modified']
        # fields = ('height', 'width')
        fields = '__all__'