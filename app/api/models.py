from uuid import uuid4

from django.db import models

from . import utils


class Replay(models.Model):
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

        ip (models.GenericIPAddressField): Sender's IPv4, necessary for
            blocking the user, when sending invalid replays frequently

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
    ip = models.GenericIPAddressField(protocol='IPv4')

    # Fields, filled after replay upload
    date_end = models.DateTimeField(null=True)
    replay = models.TextField(blank=True)
    score = models.SmallIntegerField(null=True)

    # Fields, filled after replay validation
    choices = [
        ('1', 'Waiting'),      # Replay has been created, waiting for upload
        ('1.1', 'Expired'),    # Replay hasn't been uploaded for a certain time
        ('1.2', 'Invalid'),    # Replay has been uploaded, but failed validation check
        ('2', 'Queued'),       # Replay has been queued for verification
        ('3', 'Replaying'),    # Replay is reproduced and verified
        ('3.1', 'Forged'),     # Received score doesn't correspond to the declared one
        ('4', 'Moderating'),   # Passed automatic verification, awaiting human verification
        ('4.1', 'Banned'),     # Replay has been banned for violation
        ('4.2', 'Approved')    # Replay has been approved
    ]
    status = models.CharField(
        max_length=3,
        choices=choices,
        default=choices[0][0]
    )

    def __str__(self):
        return f'"{self.nick}": {self.score}, {[v for k, v in self.choices if k == self.status][0]}'
