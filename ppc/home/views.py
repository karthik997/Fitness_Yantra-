from django.shortcuts import render
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    a = [1,2,3,4,24,1,3]
    plt.figure(figsize=(12,3))
    plt.plot(a)
    plt.savefig('./static/weight.jpg')
    plt.close()
    a = [-2,-3,-1,0,3,5,-7]
    names = ['a','b','c','d','e','f','g']
    plt.figure(figsize=(12,3))
    plt.bar(names,a)
    plt.savefig('./static/loss.jpg')
    plt.close()
    return render(request,'index.html')
