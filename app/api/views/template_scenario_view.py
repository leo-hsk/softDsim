from deprecated.classic import deprecated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.template_scenario_model import TemplateScenario
from app.serializers.template_scenario_serializer import TemplateScenarioSerializer


class TemplateScenarioView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, scenario_id=None, format=None):

        try:
            if scenario_id:
                template_scenario = TemplateScenario.objects.get(id=scenario_id)
                serializer = TemplateScenarioSerializer(template_scenario, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)

            template_scenarios = TemplateScenario.objects.all()
            serializer = TemplateScenarioSerializer(template_scenarios, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": "something went wrong on server side (except clause)"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):

        try:
            serializer = TemplateScenarioSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "Template Scenario saved", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                print(serializer.errors)
                return Response(
                    {"status": "Data is not valid", "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"status": "something went wrong internally"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, scenario_id=None):

        try:
            template_scenario = get_object_or_404(TemplateScenario, id=scenario_id)
            serializer = TemplateScenarioSerializer(template_scenario)
            template_scenario.delete()

            return Response(
                {
                    "status": "delete successful",
                    "data": {"name": serializer.data.get("name")},
                }
            )

        except:
            return Response(
                {"status": "something went wrong internally"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, scenario_id=None):

        try:
            template_scenario = TemplateScenario.objects.get(id=scenario_id)
            serializer = TemplateScenarioSerializer(
                template_scenario, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data})
            else:
                return Response({"status": "error", "data": serializer.errors})

        except:
            return Response(
                {"status": "something went wrong internally"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )