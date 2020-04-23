from rest_framework import serializers

from boxing import models


class WorkOutSerializer(serializers.ModelSerializer):
    warm_up = WarmUpSerializer(read_only=True)
    rounds = RoundSerializer(many=True, read_only=True)
    core_period = CorePeriodSerializer(read_only=True)

    class Meta:
        model = models.WorkOut
        fields = ['date', 'length', 'warm_up', 'rounds', 'core_period']


class WarmUpSerializer(serializers.ModelSerializer):
    cardio_exercises = CardioExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = models.WarmUp
        fields = ['length', 'cardio_exercises']


class RoundSerializer(serializers.ModelSerializer):
    combo = ComboSerializer(read_only=True)
    burn_out = BurnOutSerializer(read_only=True)

    class Meta:
        model = models.Round
        fields = ['length', 'combo', 'burn_out']


class CorePeriodSerializer(serializers.ModelSerializer):
    core_exercises = CoreExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = models.CorePeriod
        fields = ['length', 'core_exercises']


class ComboSerializer(serializers.ModelSerializer):
    moves = MoveSerializer(many=True, read_only=True)

    class Meta:
        model = models.Combo
        fields = ['moves']


class CardioExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CardioExercise
        fields = ['name', 'audio_file']


class MoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Move
        fields = ['name', 'audio_file']


class CoreExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CoreExercise
        fields = ['name', 'audio_file']


class BurnOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BurnOut
        fields = ['name', 'audio_file']
