from django.db import models


class WorkOut(models.Model):
    """the overall workout from warmup to boxing rounds to core exercises."""
    date = models.DateTimeField(auto_now_add=True)
    length = models.IntegerField()


class BaseExercise(models.Model):
    name = models.CharField(max_length=100)
    audio_file = None


class WarmUp(models.Model):
    """the exercises that make up the warm up period."""
    workout = models.ManyToManyField(WorkOut, related_name='warm_up')


class Round(models.Model):
    workout = models.ManyToManyField(WorkOut, related_name='rounds')


class CorePeriod(models.Model):
    """a series of core exercises that make up the core workout period."""
    workout = models.ManyToManyField(WorkOut, related_name='core_period')


class Combo(models.Model):
    """a series of moves (punches or defensive) that make up a combo."""
    round = models.ManyToManyField(Round, related_name='combo')


class CardioExercise(BaseExercise):
    """the individual exercise that make up the workout and are done between rounds of boxing."""
    warm_up = models.ManyToManyField(WarmUp, null=True, related_name='cardio_exercises') # CardioExercises are also used in the inter-round period


class Move(BaseExercise):
    """the individual movement that is a piece of a combo. ex. a jab, a cross, an uppercut etc."""
    combo = models.ManyToManyField(Combo, related_name='moves')


class CoreExercise(BaseExercise):
    """an individual core exercise that is a piece of the larger core period."""
    core_period = models.ManyToManyField(CorePeriod, related_name='core_exercises')


class BurnOut(BaseExercise):
    """exercise done at the end of a round."""
    round = models.ManyToManyField(Round, related_name='burnout')
