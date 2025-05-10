# story/views/case.py
from ..models.case import Case
from ..serializers.case import CaseSerializer
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.character import Character

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()  # The queryset to fetch the cases
    #queryset.delete()
    serializer_class = CaseSerializer  # The serializer for the Case model


    def create(self, request, *args, **kwargs):
        prompt = request.data.get("prompt")
        story_id = request.data.get("story")
        p_id = request.data.get("parent", 0)

        if p_id=="" : 
            p_id = None

        print("ID : " + str(p_id))

        if not prompt or not story_id:
            return Response({"error": "Missing prompt or story ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Create empty case
        case = Case.objects.create(
            story_id=story_id,
            title="Generating...",
            description="",
            prompt="",
        )

        try:
            # Cas 1 : On a un parent, c'est la suite d'une histoire
            if p_id is not None:
                print("_____CONT________")
                ai_response = requests.post(
                    "http://ai-script-app:8050/story/add-node",
                    json={"prompt": prompt, "parent_id": p_id, "id": case.id}
                )
            else:
                # Cas 2 : C'est un debut d'histoire car pas de parents
                print("_____START________")
                ai_response = requests.post(
                    "http://ai-script-app:8050/story/add-node-start",
                    json={"prompt": prompt, "parent_id": 0, "id": case.id}
                )

            print("Reponse : " + ai_response.text)
            ai_response.raise_for_status()
            ai_data = ai_response.json()

            # Step 3: Fill in the case with AI node data
            case.prompt = ai_data.get("texte", "")
            case.title = request.data.get("title")
            case.repliques = ai_data.get("répliques")
            if(p_id != None):
                parent_case = Case.objects.get(id=p_id)
                case.parent = parent_case

            # extract characters
            for replique in case.repliques:
                Character.objects.get_or_create(
                name=replique["personnage"],
                defaults={
                    "age": None,
                    "imagepath": "",
                    "description": "",
                    "hexcolor": "",
                })
                case.characters.append(replique["personnage"])

            case.save()

        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to generate AI node: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except ValueError:
            return Response(
                {"error": "AI server returned invalid JSON"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        from ..serializers.case import CaseSerializer
        return Response(CaseSerializer(case).data, status=status.HTTP_201_CREATED)