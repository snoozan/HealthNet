from django.db import models

import datetime
from med_information.models.record import Record
from users.models import Hospital, Patient


class Statistics(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def number_admitted_patients(self):
        return Patient.objects.filter(hospital=self.hospital.id, admitted=True)

    def avg_num_visits_patient(self, patient_id):
        records = Record.objects.all()
        patient_visit = ""
        for record in records:
            patient_visit = datetime.timedelta(record.startDate, record.endDate)

    def avg_visits_length(self):
        pass

    def get_popular_prescriptions(self):
        pass

    def get_most_common_reason(self):
        pass
