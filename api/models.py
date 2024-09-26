from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_fein(value):
    if not value.isdigit() or len(value) != 9:
        raise ValidationError("FEIN must be a 9-digit number.")


class Business(models.Model):
    INDUSTRY_CHOICES = [
        ("restaurants", "Restaurants"),
        ("stores", "Stores"),
        ("wholesale", "Wholesale"),
        ("services", "Services"),
    ]

    WORKFLOW_STAGES = [
        ("new", "New"),
        ("market_approved", "Market Approved"),
        ("market_declined", "Market Declined"),
        ("sales_approved", "Sales Approved"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]

    fein = models.CharField(max_length=9, unique=True, validators=[validate_fein])
    name = models.CharField(max_length=255)
    industry = models.CharField(
        max_length=20, choices=INDUSTRY_CHOICES, null=True, blank=True
    )
    workflow_stage = models.CharField(
        max_length=20, choices=WORKFLOW_STAGES, default="new"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def progress_workflow(self, status=None):
        if self.workflow_stage == "new":
            if self.industry in ["restaurants", "stores"]:
                self.workflow_stage = "market_approved"
            else:
                self.workflow_stage = "market_declined"
        elif self.workflow_stage == "market_approved" and self.contact:
            self.workflow_stage = "sales_approved"
        elif self.workflow_stage == "sales_approved" and status in ["won", "lost"]:
            self.workflow_stage = status
        self.save()

    def get_next_step_info(self):
        if self.workflow_stage == "new":
            return "Provide industry to progress."
        elif self.workflow_stage == "market_approved":
            return "Provide contact information (name and phone) to progress to sales approved stage."
        elif self.workflow_stage == "sales_approved":
            return "Provide status ('won' or 'lost') to complete the workflow."
        elif self.workflow_stage in ["market_declined", "won", "lost"]:
            return "Workflow completed. No further steps available."
        else:
            return "Unknown stage. No information available."


class Contact(models.Model):
    business = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name="contact"
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
