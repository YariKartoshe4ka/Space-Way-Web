from uuid import uuid4

from django.db import models

from . import utils


def __replay_factory(version):
    class Metaclass(models.base.ModelBase):
        def __new__(self, name, bases, attrs):
            name += ' ' + version
            return models.base.ModelBase.__new__(self, name, bases, attrs)

    class Replay(models.Model, metaclass=Metaclass):
        """Representation of replay object

        Fields, filled on replay creation:
            id (models.UUIDField): Replay identifier. UUID4 format is used instead
                of the usual number, in order to prevent the block of someone
                else's replay (by guessing ID number)

            nick (models.CharField): Nickname of the player who owns this replay.
                Only ASCII numbers and letters are allowed, as well as some
                special characters

            date_start (models.DateTimeField): Date of replay creation. Added
                automatically to calculate the replay duration for its future
                validation

            state (models.TextField): The initial state of the `random.getstate`.
                The data is dumped via pickle and encoded in base64

        Fields, filled after replay upload:
            date_end (models.DateTimeField): End date of replay. Added to calculate
                the replay duration for its future validation

            replay (models.TextField): Replay (user actions) which are dumped via
                pickle and encoded in base64

            score (models.SmallIntegerField): The declared score, which must be
                confirmed after replay validation

        Fields, filled after replay validation:
            status (models.CharField): The verdict of the replay verification

        """
        # Fields, filled on replay creation
        id = models.UUIDField(
            primary_key=True,
            default=uuid4,
            editable=False
        )
        nick = models.CharField(max_length=15)
        date_start = models.DateTimeField(auto_now_add=True)
        state = models.TextField(
            default=utils.random_getstate,
            editable=False
        )

        # Fields, filled after replay upload
        date_end = models.DateTimeField(null=True)
        replay = models.TextField(blank=True)
        score = models.SmallIntegerField(null=True)

        # Fields, filled after replay validation
        choices = [
            ('waiting', 'Waiting'),        # Replay has been created, waiting for upload
            ('invalid', 'Invalid'),        # Replay has been uploaded, but failed validation check
            ('queued', 'Queued'),          # Replay has been queued for verification
            ('replaying', 'Replaying'),    # Replay is reproduced and verified
            ('forged', 'Forged'),          # Received score doesn't correspond to the declared one
            ('approved', 'Approved'),      # Replay has been approved
            ('outdated', 'Outdated')       # Replay has been replaced with a newer one
        ]
        status = models.CharField(
            max_length=15,
            choices=choices,
            default=choices[0][0]
        )

        class Meta:
            db_table = 'api_v' + version
            ordering = ['-date_start']
            verbose_name = 'Replay ' + version
            verbose_name_plural = verbose_name

        def __str__(self):
            return f'"{self.nick}": {self.score}, {self.status}'

    return Replay


versions = ['2.2.0']
__replay_models = {}

for version in versions:
    __replay_models[version] = __replay_factory(version)

__replay_models['latest'] = __replay_models[versions[-1]]


def get_replay_model(version):
    return __replay_models.get(version) or __replay_models['latest']
