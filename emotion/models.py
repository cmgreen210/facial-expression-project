from django.db import models


class ClassificationRequest(models.Model):

    timestamp = models.DateTimeField(auto_now=True)

    # 0 - video upload
    # 1 - image upload
    type = models.PositiveIntegerField()


class ImageClassification(models.Model):

    request = models.ForeignKey('ClassificationRequest')

    # String of pixels comma separated (48 x 48) image
    image = models.TextField()

    # Rank 
    rank1 = models.PositiveIntegerField()
    rank1_prob = models.CharField(max_length=15)()

    rank2 = models.PositiveIntegerField()
    rank2_prob = models.CharField(max_length=15)()

    rank3 = models.PositiveIntegerField()
    rank3_prob = models.CharField(max_length=15)()

    rank4 = models.PositiveIntegerField()
    rank4_prob = models.CharField(max_length=15)()

    rank5 = models.PositiveIntegerField()
    rank5_prob = models.CharField(max_length=15)()

    rank6 = models.PositiveIntegerField()
    rank6_prob = models.CharField(max_length=15)()

    rank7 = models.PositiveIntegerField()
    rank7_prob = models.CharField(max_length=15)()
