from rest_framework import serializers
from .models import Business, Contact
from django.core.exceptions import ObjectDoesNotExist


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "phone"]


class BusinessSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(required=False)
    next_step = serializers.SerializerMethodField()
    status = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Business
        fields = [
            "id",
            "fein",
            "name",
            "industry",
            "workflow_stage",
            "contact",
            "next_step",
            "status",
        ]
        read_only_fields = ["id", "workflow_stage", "next_step"]

    def get_next_step(self, obj):
        return obj.get_next_step_info()

    def validate(self, data):
        instance = self.instance
        if instance:
            current_stage = instance.workflow_stage
            if current_stage == "new" and not ("industry" in data or instance.industry):
                raise serializers.ValidationError(
                    "Industry is required to progress from new state."
                )
            elif current_stage == "market_approved":
                contact_exists = False
                try:
                    contact_exists = instance.contact is not None
                except ObjectDoesNotExist:
                    pass

                if not (data.get("contact") or contact_exists):
                    raise serializers.ValidationError(
                        "Contact information is required to progress from market approved state."
                    )
            elif current_stage == "sales_approved" and "status" not in data:
                raise serializers.ValidationError(
                    "Status is required to progress from sales approved state."
                )
            elif current_stage == "sales_approved" and data.get("status") not in [
                "won",
                "lost",
            ]:
                raise serializers.ValidationError(
                    "Invalid status. Must be 'won' or 'lost'."
                )
        return data

    def create(self, validated_data):
        contact_data = validated_data.pop("contact", None)
        business = Business.objects.create(**validated_data)
        if contact_data:
            Contact.objects.create(business=business, **contact_data)
        return business

    def update(self, instance, validated_data):
        contact_data = validated_data.pop("contact", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if contact_data:
            contact, created = Contact.objects.get_or_create(business=instance)
            for attr, value in contact_data.items():
                setattr(contact, attr, value)
            contact.save()

        instance.save()

        status = validated_data.pop("status", None)
        instance.progress_workflow(status=status)

        return instance
