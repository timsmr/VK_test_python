from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, RequestSerializer, FriendSerializer
from .models import User, Request, Friend
from drf_yasg.utils import swagger_auto_schema

class CustomUser(APIView):
    """Get user info"""

    @swagger_auto_schema(responses={200: 'Get user info'})
    def get(self, request, pk):
        """Get user info"""
        user = User.objects.get(pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomUserCreate(APIView):
    """Create new user"""

    @swagger_auto_schema(responses={201: 'Friend had been created', 400: 'Wrong data'})
    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateRequest(APIView):
    """Create friend request"""

    @swagger_auto_schema(responses={200: 'Got incoming request. Create friend instance', 201: 'Friend request had been created', 400: 'Wrong data'})
    def post(self, request, sender, receiver):
        """Create friend request"""

        # if incoming request then create a friend instance and delete incoming request
        if Request.objects.get(sender=receiver):
            serializer_sender = FriendSerializer(data={'user': sender, 'friend': receiver})
            serializer_receiver = FriendSerializer(data={'user': receiver, 'friend': sender})
            if serializer_sender.is_valid() and serializer_receiver.is_valid():
                serializer_sender.save()
                serializer_receiver.save()

                Request.objects.get(sender=receiver).delete()

                return Response('Got an incoming request. You`re friends now!', status=status.HTTP_200_OK)

        else:
            data = {'sender': sender, 'receiver': receiver}
            serializer = RequestSerializer(data=data) 
            if serializer.is_valid():
                request = serializer.save()
                if request:
                    json = serializer.data
                    return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HandleAcceptDecline(APIView):
    """Declines friend request if /decline/ and Accepts friend request if /accept/"""

    @swagger_auto_schema(responses={200: 'Accepted or Declined request successfully', 400: 'Wrong data'})
    def put(self, request, sender, receiver):
        """Update decline field in request if /decline/ or create friend instances if /accept/"""
        req = Request.objects.get(sender=sender, receiver=receiver)
        if request.path.split('/')[-2] == 'accept':
            serializer_sender = FriendSerializer(data={'user': sender, 'friend': receiver})
            serializer_receiver = FriendSerializer(data={'user': receiver, 'friend': sender})
            if serializer_sender.is_valid() and serializer_receiver.is_valid():
                serializer_sender.save()
                serializer_receiver.save()

                req.delete()

                return Response('You`re friends now!', status=status.HTTP_200_OK)
        else:
            serializer = RequestSerializer(req, data={'sender': sender, 'receiver': receiver, 'declined': True})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HandleOutgoingIncomingRequests(APIView):
    """Get outgoing requests of user if /outgoing/ and get incoming requests if /incoming/"""

    @swagger_auto_schema(responses={200: 'Got list of requests'})
    def get(self, request, user):
        """Get list of outgoing requests of user if /outgoing/ and Get list of incoming requests if /incoming/"""
        if request.path.split('/')[-2] == 'outgoing':
            req = Request.objects.filter(sender=user)
            serializer = RequestSerializer(req, many=True)
        else:
            req = Request.objects.filter(receiver=user)
            serializer = RequestSerializer(req, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetFriends(APIView):
    """Get all friends of user"""

    @swagger_auto_schema(responses={200: 'Got list of friends'})
    def get(self, request, pk):
        """Get friends list"""
        friends = Friend.objects.filter(user=pk)
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StatusFriend(APIView):
    """Get friend status if /status/ and Deletes friend if /delete/"""

    @swagger_auto_schema(responses={200: 'Got friend status'})
    def get(self, request, sender, receiver):
        """Get friend status"""
        if Friend.objects.get(user=sender, friend=receiver):
            return Response('Friends', status=status.HTTP_200_OK)
        elif Request.objects.get(sender=sender, receiver=receiver):
            return Response('Got outgoing request', status=status.HTTP_200_OK)
        elif Request.objects.get(sender=receiver, receiver=sender):
            return Response('Got incoming request', status=status.HTTP_200_OK)
        else:
            return Response('Nothing', status=status.HTTP_200_OK)
    
class DeleteFriend(APIView):
    """Delete friend"""

    @swagger_auto_schema(responses={204: 'Friend had been deleted', 400: 'This people are not friends'})
    def delete(self, request, sender, receiver):
        """Deletes friend"""
        send_friend = Friend.objects.get(user=sender, friend=receiver)
        res_friens = Friend.objects.get(user=receiver, friend=sender)
        if send_friend and res_friens:
            send_friend.delete()
            res_friens.delete()
            return Response('Deleted', status=status.HTTP_204_NO_CONTENT)
        
        return Response('This people are not friends', status=status.HTTP_400_BAD_REQUEST)
        