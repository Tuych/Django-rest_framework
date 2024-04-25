from rest_framework import serializers
from .models import Todo, Movie


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['task', 'timestamp', 'update', 'complated']


#phone_number validate to UZB --> number
import re

def is_phone_number_valid(phone_number):

    pattern = re.compile(r'^\+998\d{9}$')

    if re.match(pattern, phone_number):
        return phone_number
    else:
        raise serializers.ValidationError('Telefon raqamini +998XX0000000 formatda kiriting')





class MovieSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[is_phone_number_valid])

    
    class Meta:
        model = Movie
        fields = '__all__'


    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Reting 1 va 10 oralig'ida bo'lishi kerak")
        return value
    

    def validate(self, attrs):
        if attrs['uzb_gross'] > attrs['world_gross']:
            print('-----------', attrs['uzb_gross'], attrs['world_gross'])
            raise serializers.ValidationError(" uzb_gross world_gross dan kichik bo'lishi kerak")
        return attrs
    


