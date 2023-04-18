from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError('kh co email')
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self,email,name,password=None):
        if not email:
            raise ValueError('kh co email')
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()

        return user
    


class UserAccount(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    
    
    def get_short_name(self):
        return self.name
    
    
    def __str__(self):
        return self.id

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(UserAccount, related_name='user1', on_delete=models.CASCADE, null=True, blank=True)
    user2 = models.ForeignKey(UserAccount, related_name='user2', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default='waiting')
    turn = models.ForeignKey(UserAccount, related_name='turn', on_delete=models.CASCADE, null=True, blank=True)
    winner = models.ForeignKey(UserAccount, related_name='winner', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id

class Move(models.Model):
    # id = models.AutoField(primary_key=True,default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    move_type = models.CharField(max_length=1)
    x = models.IntegerField()
    y = models.IntegerField()

    def get_board(self):
        return [[int(cell) for cell in row.split(',')] for row in self.board.split(';')]

    def set_board(self, board):
        self.board = ';'.join([','.join([str(cell) for cell in row]) for row in board])

    def make_move(self, x, y, move_type):
        board = self.get_board()
        board[x][y] = move_type
        self.set_board(board)
        self.save()
    

class Board(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, primary_key=True)
    board = models.TextField(default='')
    SIZE = 16

    def __init__(self):
        self.board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.moves = []

    def make_move(self, x, y, player):
        self.board[x][y] = player
        self.moves.append((x, y, player))

    def get_moves(self):
        return self.moves

    def check_win(self, x, y, player):
        # Kiểm tra hàng dọc
        count = 0
        for i in range(self.SIZE):
            if self.board[x][i] == player:
                count += 1
            else:
                count = 0
            if count == 5:
                return True

        # Kiểm tra hàng ngang
        count = 0
        for i in range(self.SIZE):
            if self.board[i][y] == player:
                count += 1
            else:
                count = 0
            if count == 5:
                return True

        # Kiểm tra đường chéo chính
        count = 0
        start_x = max(x, y) - min(x, y)
        start_y = max(x, y) - start_x
        while start_x < self.SIZE and start_y < self.SIZE:
            if self.board[start_x][start_y] == player:
                count += 1
            else:
                count = 0
            if count == 5:
                return True
            start_x += 1
            start_y += 1

        # Kiểm tra đường chéo phụ
        count = 0
        start_x = x + y
        start_y = y - x
        while start_x >= 0 and start_x < self.SIZE and start_y >= 0 and start_y < self.SIZE:
            if self.board[start_x][start_y] == player:
                count += 1
            else:
                count = 0
            if count == 5:
                return True
            start_x -= 1
            start_y += 1

        return False

# Create your models here.
