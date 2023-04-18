from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room, Move, Board
from .serializers import RoomSerializer, MoveSerializer, BoardSerializer
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def list_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_room(request):
    room = Room()
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
@authentication_classes([])
@permission_classes([AllowAny])
def make_move(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.turn != request.user:
        return Response({'message': 'It is not your turn'})
    x = request.data.get('x')
    y = request.data.get('y')
    move = Move(user=request.user, room=room, move_type='X', x=x, y=y)
    move.save()
    board = Board.objects.get(room=room)
    board.board[x*16+y] = 'X'
    board.save()
    # check for win condition
    # switch turn
    serializer = MoveSerializer(move)
    return Response(serializer.data)
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quit_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.user1 == request.user:
        room.user1 = None
        room.status = 'waiting'
        room.turn = None
        room.winner = room.user2
        room.save()
    elif room.user2 == request.user:
        room.user2 = None
        room.status = 'waiting'
        room.turn = None
        room.winner = room.user1
        room.save()
    else:
        return Response({'message': 'You are not in this room'})
    return Response({'message': 'You have left the room'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_board(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.status != 'playing':
        return Response({'message': 'This room is not available for playing'})
    user = request.user
    if user != room.turn:
        return Response({'message': 'It is not your turn to play'})
    x = int(request.POST.get('x'))
    y = int(request.POST.get('y'))
    if x < 0 or x > 15 or y < 0 or y > 15:
        return Response({'message': 'Invalid move'})
    move_type = request.POST.get('move_type')
    if move_type not in ['X', 'O']:
        return Response({'message': 'Invalid move'})
    move = Move(room=room, user=user, x=x, y=y, move_type=move_type)
    move.save()
    board = room.board
    board[x][y] = move_type
    if Board.check_win(board, x, y):
        room.status = 'finished'
        room.winner = user
    else:
        if move_type == 'X':
            room.turn = room.user2
        else:
            room.turn = room.user1
    room.save()
    serializer = RoomSerializer(room)
    return Response(serializer.data)