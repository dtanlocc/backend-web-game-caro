from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room, Move, Board, UserAccount
from .serializers import RoomSerializer, MoveSerializer, BoardSerializer
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from channels.layers import get_channel_layer
import json
from django.http import HttpResponse

@api_view(['GET'])
# @authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def list_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def create_room(request):
    room = Room()
    room.save()
    room.create_board()
    room.save()
    serializer = RoomSerializer(room)
    return Response(serializer.data)

# @api_view(['POST'])
# def join_room(request, room_id):
#     room = Room.objects.get(id=room_id)
#     room.user2 = request.user
#     room.status = 'started'
#     room.turn = room.user1
#     room.save()
#     serializer = RoomSerializer(room)
#     return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def make_move(request, room_id):
    room = Room.objects.get(id=room_id)
    # print(room.turn)
    # print(request.user.id)
    if room.turn != request.user:
        return Response({'message': 'It is not your turn'})
    move_type = "O"
    if room.user1 == request.user:
        move_type = "X"
    x = int(request.data.get('x'))
    y = int(request.data.get('y'))
    # move = Move(user=request.user, room=room, move_type=move_type, x=x, y=y)
    
    # move.save()
    board = Board.objects.get(room=room)
    # board.board[x*16+y] = 'X'
    # print('x: ',x,'y:',y)
    data = board.make_move(x,y,move_type)
    # board.save()
    
    
    if board.check_win(x,y,move_type):
        if move_type =="X":
            room.winner = room.user1
        else:
            room.winner=room.user2
    
    board.save()
    if room.turn == room.user1:
        room.turn = room.user2
    else:
        room.turn = room.user1
    # room.save()
    
    room.save()
    # check for win condition
    # switch turn
    # serializer = MoveSerializer(move)
    # board.save()
    # sio.emit('update_board', {}, room=room_id)

    return Response(data)
# 
# @api_view(['POST'])
# def create_room(request):
#     user = request.user
#     if not user.is_authenticated:
#         return Response({'message': 'You must be logged in to create a room'})
#     # check if user already has a room
#     user_rooms = Room.objects.filter( Q(user1=user) | Q(user2=user)).exclude(status='finished')
#     if user_rooms.exists():
#         return Response({'message': 'You are already in a room'})
#     room = Room(user1=user, status='waiting')
#     room.save()
#     serializer = RoomSerializer(room)
#     return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_room(request, room_id):
    user = request.user
    if not user.is_authenticated:
        return Response({'message': 'You must be logged in to join a room'})
    room = Room.objects.get(id=room_id)
    if room.status != 'waiting':
        return Response({'message': 'This room is not available for joining'})
    if room.user1 is None:
        room.user1 = user
        room.status = 'waiting'
    else:
        if room.user1 == user:
            return Response({'message': 'You cannot join a room that you created'})
        room.user2 = user
        room.status = 'started'
        room.turn = room.user1
    room.save()
    serializer = RoomSerializer(room)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def update_board(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.user.id != room.user1.id and request.user.id != room.user2.id:
        return Response({'message': 'jjjjj'})
    board = Board.objects.get(room=room)
    
    data = {
            "board":board.board,
            # 'turn':room.turn,
            "winner": room.winner.id if room.winner else None
            }
    # json_data = json.dumps(data)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reset_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.user != room.user1 and request.user != room.user2:
        return Response({'message': 'none'})
    elif request.user == room.user1:
        room.user1 = None
    else:
        room.user2 = None
    room.reset_room()
    room.save()
    data = {
        "message": "success"
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    # room.save()
    return Response({'message': 'delete'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quit_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.user1 == request.user:
        room.user1 = None
        room.status = 'waiting'
        room.turn = None
        room.winner = room.user2
        # room.save()
    elif room.user2 == request.user:
        room.user2 = None
        room.status = 'waiting'
        room.turn = None
        room.winner = room.user1
        # room.save()
    else:
        return Response({'message': 'You are not in this room'})
    return Response({'message': 'You have left the room'})
