from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Project, Review
from .serializers import ProjectSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['title', 'owner__username', 'owner__profile__domain']  
    ordering_fields = '__all__'
    ordering = ['created_at']  
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  
        return [AllowAny()] 

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(owner__username__icontains=search_term) |
                Q(owner__profile__domain__icontains=search_term)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  
        
        
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = permission_classes = [IsOwnerOrReadOnly] 



class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    