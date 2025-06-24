import torch
import torch.nn.functional as f
import torch.nn as nn
import torch.utils.data.dataset as dataset
import os


class BotNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(7,64) #входной слой из 7 параметров:player_x, player_dx, bullet_x, bullet_y, bullet_dy, bot_x, bot_dx -> скрытый слой 1
        self.fc2 = nn.Linear(64,64) #скрытый слой 1 -> скрытый слой 2
        self.move = nn.Linear(64,3) #скрытый слой 2 -> выходной слой move
        self.shoot = nn.Linear(64, 2) #скрытый слой 2 -> выходной слой shoot
    #Обязательнй метод, наследованный от nn.Module, прямой проход
    def forward(self,x):
        #ReLu - универсальная активационная функция, bias по умолчанию - True
        x = f.relu(self.fc1(x))
        x = f.relu(self.fc2(x))
        return self.move(x), self.shoot(x) #Линейная функция на выходных нейронах
    @staticmethod
    def train_model(model, dataloader, epochs = 10, lr = 0.01):
        #Оптимизатор Adam
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        #Функция потерь nn.CrossEntropyLoss() - подходит для задач классификации с ReLu скрытыми слоями и Linear на выходе
        loss_fn_move = nn.CrossEntropyLoss()
        loss_fn_shoot = nn.CrossEntropyLoss()

        for epoch in range(epochs):
            total_loss = 0
            for X,Y in dataloader: #X - входные значения, Y - ожидаемые действия
                move_targets = Y[:,0].long() #ожидмаемый класс движения (0,1 или 2 (влево, стоять, вправо))
                shoot_targets = Y[:, 1].long() #ожидаемый класс стрельбы (0 или 1)

                # Прямой прогон модели, получение значений предсказанных моделью
                move_logits, shoot_logits = model(X)

                #Вычисление потерь
                loss_move = loss_fn_move(move_logits, move_targets)
                loss_shoot = loss_fn_shoot(shoot_logits, shoot_targets)
                loss = loss_move+loss_shoot

                #Градиентный спуск, корректировка весов model.parameters()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
