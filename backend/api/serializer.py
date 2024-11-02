from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
#from rest_framework.validators import UniqueValidator
#from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api import models as api_models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):: This line creates a new token serializer called MyTokenObtainPairSerializer that is based on an existing one called TokenObtainPairSerializer. Think of it as customizing the way tokens work.
    @classmethod: This line indicates that the following function is a class method, which means it belongs to the class itself and not to an instance (object) of the class.
    def get_token(cls, user):: This is a function (or method) that gets called when we want to create a token for a user. The user is the person who's trying to access something on the website.
    token = super().get_token(user): Here, it's asking for a regular token from the original token serializer (the one it's based on). This regular token is like a key to enter the website.
    token['full_name'] = user.full_name, token['email'] = user.email, token['username'] = user.username: This code is customizing the token by adding extra information to it. For example, it's putting the user's full name, email, and username into the token. These are like special notes attached to the key.
    return token: Finally, the customized token is given back to the user. Now, when this token is used, it not only lets the user in but also carries their full name, email, and username as extra information, which the website can use as needed.
    '''

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        return token


# Define a serializer for user registration, which inherits from serializers.ModelSerialize

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        # Corrija o nome para "model"
        model = api_models.User  # Certifique-se de que api_models.User é um modelo válido
        fields = ['full_name', 'email',  'password', 'password2']

    def validate(self, attrs):
        # Verifique se as senhas coincidem
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        # Remova o campo password2 pois ele não faz parte do modelo
        validated_data.pop('password2')
        
        # Crie o usuário com os campos restantes
        user = api_models.User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )

        # Defina o username e a senha do usuário
        email_username, _ = user.email.split('@')
        user.username = email_username
        user.set_password(validated_data['password'])
        
        # Salve o usuário e retorne a instância criada
        user.save()
        return user


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = "__all__"


class ProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model = api_models.Profile
        fields = "__all__"


class CategorySerializer (serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    '''
        category.post_set: In Django, when you define a ForeignKey relationship from one model to another 
        (e.g., Post model having a ForeignKey relationship to the Category model), 
        Django creates a reverse relationship from the related model back to the model that has the ForeignKey. 
        By default, this reverse relationship is named <model>_set. In this case, since the Post model has a 
        ForeignKey to the Category model, Django creates a reverse relationship from Category to Post named post_set. 
        This allows you to access all Post objects related to a Category instance.
    '''
    def get_post_count(self, category):
         return category.post_set.count()  # Modificado para post_set
    
    class Meta:
        model = api_models.Category
        fields = [
            "id",
            "title",
            "image",
            "slug",
            "post_count",
        ]


class  CommentSerializer (serializers.ModelSerializer):

    class Meta:
        model = api_models.Comment
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1


class  PostSerializer (serializers.ModelSerializer):

    class Meta:
        model = api_models.Post
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1


class  BookmarkSerializer (serializers.ModelSerializer):

    class Meta:
        model = api_models.Bookmark
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(BookmarkSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1


class  NotificationSerializer (serializers.ModelSerializer):

    class Meta:
        model = api_models.Notification
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1


class AuthorSerializer(serializers.Serializer):
    views = serializers.IntegerField(default=  0)
    post = serializers.IntegerField(default=  0)
    likes = serializers.IntegerField(default=  0)
    bookmarks = serializers.IntegerField(default=  0)
