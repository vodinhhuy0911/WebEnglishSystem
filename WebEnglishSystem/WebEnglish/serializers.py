from rest_framework.serializers import ModelSerializer
from .models import Category, User, Answers, MultipleChoice


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UserSerializers(ModelSerializer):

    def create(self, validated_data):
        user =  User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name","username","password","email","date_joined"]
        extra_kwargs ={
            'password':{'write_only':'true'}
        }

class AnswerSeralizers(ModelSerializer):
    class Meta:
        model = Answers
        fields = ["id","answer"]

class MultipleChoiceSerializers(ModelSerializer):
    answers   = AnswerSeralizers(many=True)
    class Meta:
        model = MultipleChoice
        fields = ["id","content","answer_correct","answers"]
