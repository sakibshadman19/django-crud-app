from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Parent, Child
from .serializers import ParentSerializer, ChildSerializer

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    
    # Handle creation of a Parent instance
    def create(self, request, *args, **kwargs):
        required_fields = ['first_name', 'last_name', 'street', 'city', 'state', 'zip_code'] 
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response(
                {'error': f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle retrieval of a Parent instance by primary key
    def retrieve(self, request, pk=None):
        try:
            parent = self.get_queryset().get(pk=pk)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(parent)
        return Response(serializer.data)

    # Handle updating a Parent instance by primary key
    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', True)

        try:
            parent = self.get_queryset().get(pk=pk)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent not found. Please create the parent first.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(parent, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request,pk, *args, **kwargs):
        try:
            parent = self.get_queryset().get(pk=pk)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Prevent deletion if the parent has children
        if parent.children.exists():
            return Response(
                {"error": "Cannot delete parent with existing children."},
                status=status.HTTP_400_BAD_REQUEST
            )
        parent.delete()
        return Response({'message': 'Parent deleted successfully.'}, status=status.HTTP_200_OK)

class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    # Handle creation of a Child instance
    def create(self, request, *args, **kwargs):
        required_fields = ['first_name', 'last_name', 'parent']
        missing_fields = [field for field in required_fields if field not in request.data]

        if missing_fields:
            return Response(
                {'error': f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        parent_data = request.data.get('parent')
        if parent_data:
            try:
                if isinstance(parent_data, int):
                    parent = Parent.objects.get(pk=parent_data)
            except Parent.DoesNotExist:
                return Response({'error': 'Parent not found.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle retrieval of a Child instance by primary key
    def retrieve(self, request, pk=None):
        try:
            child = self.get_queryset().get(pk=pk)
        except Child.DoesNotExist:
            return Response({'error': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(child)
        return Response(serializer.data)

    # Handle updating a Child instance by primary key
    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', True)  
        try:
            child = self.get_queryset().get(pk=pk)
        except Child.DoesNotExist:
            return Response({'error': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)

        parent_data = request.data.get('parent')
        if parent_data:
            try:
                if isinstance(parent_data, int):
                    parent = Parent.objects.get(pk=parent_data)
                child.parent = parent 
            except Parent.DoesNotExist:
                return Response({'error': 'Parent not found.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(child, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    # Handle deletion of a Child instance by primary key
    def destroy(self, request, pk, *args, **kwargs):
        try:
            child = self.get_queryset().get(pk=pk)
        except Child.DoesNotExist:
            return Response({'error': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)
        child.delete()

        return Response({'message': 'Child deleted successfully.'}, status=status.HTTP_200_OK)


