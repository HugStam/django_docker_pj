from rest_framework import serializers
from tours_db.models import Customers


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('id', 'f_name', 'l_name', 'description',
                  'published')
