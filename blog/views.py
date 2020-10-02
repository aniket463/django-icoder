from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    # print(allPosts)
    context = {"allPosts":allPosts}
    return render(request, 'blog/blogHome.html',context)


def blogSlug(request, slug):
    post=Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replayDict = {}
    for replay in replies:
        if replay.parent.sno not in replayDict.keys():
            replayDict[replay.parent.sno] = [replay]
        else:
            replayDict[replay.parent.sno].append(replay)
    print(replayDict)
    # print(comments,replies)
    #print(request.user)
    context = {"post":post,'comments':comments,'user':request.user,'replayDict':replayDict}
    return render(request, 'blog/blogPost.html',context)



def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")

        if parentSno == "":
            comment = BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Your Comment has posted Successfully")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Your replay has posted Successfully")
  
    return redirect(f"/blog/{post.slug}")
