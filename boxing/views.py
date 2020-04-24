from rest_framework.generics import CreateAPIView

from boxing.serializers import WorkOutSerializer
from boxing.workout_creator import create_workout


class WorkOutView(CreateAPIView):
    serializer_class = WorkOutSerializer

    def create(self, serializer):
        return create_workout()
