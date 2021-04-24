from django.db import models

# Create your models here.
class DataTerminal(models.Model):
    SW = models.TextField()
    T1 = models.IntegerField()
    T2 = models.IntegerField()
    T3 = models.IntegerField()
    T4 = models.IntegerField()
    T5 = models.IntegerField()
    TS = models.IntegerField()
    status = models.IntegerField(null=True)

    class Meta:
        db_table = "data_terminal"

class AlertReport(models.Model):
    SW = models.TextField()
    data = models.ForeignKey(DataTerminal,  on_delete=models.CASCADE,  null=True)
    alert_type = models.TextField(default="Ping Lost")
    alert_datetime = models.IntegerField()
    email_alert_datetime = models.IntegerField(null=True)

    class Meta:
        db_table = "alert_report"