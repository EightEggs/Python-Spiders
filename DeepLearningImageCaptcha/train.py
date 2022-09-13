import os
import torch
import torch.nn as nn
from torch.autograd import Variable
import dataset
from model import CNN
from evaluate import main as evaluate

num_epochs = 64
batch_size = 128
learning_rate = 0.001


def main():
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    cnn = CNN()
    cnn.cuda()
    cnn.train()

    criterion = nn.MultiLabelSoftMarginLoss()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=learning_rate)
    max_eval_acc = -1

    train_dataloader = dataset.get_train_data_loader()
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_dataloader):
            images = Variable(images).cuda()
            labels = Variable(labels.float()).cuda()
            predict_labels = cnn(images)
            loss = criterion(predict_labels, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if (i + 1) % 10 == 0:
                print("epoch:", epoch, "step:", i, "loss:", loss.item())
            if (i + 1) % 100 == 0:
                # current is model.pkl
                torch.save(cnn.state_dict(), "./model.pkl")
                print("save model")
        print("epoch:", epoch, "step:", i, "loss:", loss.item())
        eval_acc = evaluate()
        if eval_acc > max_eval_acc:
            # best model save as best_model.pkl
            torch.save(cnn.state_dict(), "./best_model.pkl")
            print("save best model")
    torch.save(cnn.state_dict(), "./model.pkl")
    print("save last model")


if __name__ == '__main__':
    main()
