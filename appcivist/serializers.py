from rest_framework import serializers
from appcivist.models import Campaign, Author, Theme, Idea, Comment, Feedback

# class AssemblySerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='appcivist_id', read_only=True)
#     community = serializers.IntegerField(source='appcivist_id', read_only=True)
#     class Meta:
#         model = Assembly
#         exclude = ('appcivist_id', 'appcivist_uuid', 'resource_space_id', 
#                    'forum_resource_space_id', 'admin_session_key', 
#                    'admin_email', 'admin_password', 'session_key_last_update', 
#                    'session_key_longevity_days')

class CampaignSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='appcivist_id', read_only=True)
    community = serializers.IntegerField(source='appcivist_id', read_only=True)
    class Meta:
        model = Campaign
        exclude = ('appcivist_id', 'appcivist_uuid', 'resource_space_id', 
                   'forum_resource_space_id', 'admin_session_key', 'assembly_id',
                   'admin_email', 'admin_password', 'session_key_last_update', 
                   'session_key_longevity_days')


# class CampaignSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='appcivist_id', read_only=True)

#     class Meta:
#         model = Campaign
#         exclude = ('appcivist_uuid', 'resource_space_id', 'forum_resource_space_id', 'assembly')

class ThemeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='appcivist_id', read_only=True)

    class Meta:
        model = Theme
        exclude =  ('campaign', 'description', 'theme_type')

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='appcivist_id', read_only=True)

    class Meta:
        model = Author
        exclude = ('appcivist_id', 'appcivist_uuid', 'sync', 'campaign', 'source')


class IdeaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='appcivist_id', read_only=True)
    user_info = AuthorSerializer(source='user', read_only=True)
    #location_info = LocationSerializer(source='location', read_only=True)
    campaign_info = ThemeSerializer(source='theme', read_only=True)

    class Meta:
        model = Idea
        exclude = ('appcivist_id', 'sync', 'user', 'theme', 'appcivist_uuid',
                   'resource_space_id', 'forum_resource_space_id')


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='appcivist_id', read_only=True)
    user_info = AuthorSerializer(source='user', read_only=True)
    #location_info = LocationSerializer(source='location', read_only=True)
    parent_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        exclude = ('appcivist_id', 'user', 'parent_idea', 'parent_comment', 'sync',
                   'resource_space_id', 'forum_resource_space_id')


class FeedbackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='appcivist_id', read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    parent_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Feedback
        exclude = ('appcivist_id', 'sync', 'author', 'parent_idea', 'parent_comment')
