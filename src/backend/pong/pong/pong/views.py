# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/17 18:36:34 by jaizpuru          #+#    #+#              #
#    Updated: 2024/10/24 11:34:42 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from requests.sessions import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PongGameStateSerializer, PongGameSerializer, Tournament4PSerializer, Tournament4PStateSerializer, Tournament8PSerializer
from .models import Player

User = get_user_model()

class CreateDefaultPlayerView(APIView):
    
    def post(self, request: Request, pk) -> Response:
        player_data = request.data;
        player, created = Player.objects.get_or_create(
            id=pk,
            defaults={
                'name': player_data['name'],
                'scores': [], 
                'total_games': 0,
                'total_score': 0,
            }
        )
        if not created:
            raise Exception("Player already exists")
        response = {
            "message": "Player created successfully",
            "status": status.HTTP_201_CREATED,
            "player_id": player.id,
        }
        return Response(response, status=status.HTTP_201_CREATED)

class PostGameView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = PongGameSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
        
class PostGameStateView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = PongGameStateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class Tournament4PView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = Tournament4PSerializer(data=request.data)

        if serializer.is_valid():
            tournament = serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "tournament_id": tournament.id,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
        
class Tournament4PStateView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = Tournament4PStateSerializer(data=request.data)

        if serializer.is_valid():
            tournament = serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "tournament_id": tournament.id,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class Tournament8P(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = Tournament8PSerializer(data=request.data)

        if serializer.is_valid():
            tournament = serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "tournament_id": tournament.id,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )