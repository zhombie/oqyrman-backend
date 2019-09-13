from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer
from .forms import BookForm


def book_create(request):
    form = BookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "book_form.html", context)


def book_list(request):
    queryset_list = Book.objects.all()
    paginator = Paginator(queryset_list, 12)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List of books",
        "page_request_var": page_request_var,
    }
    return render(request, "book_list.html", context)


def book_section_list(request, pk=None):
    queryset_list = Book.objects.filter(section_id=pk)
    context = {
        "object_list": queryset_list,
        }
    return render(request, "book_list.html", context)


def book_detail(request, id=None):
    instance = get_object_or_404(Book, id=id)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "book_detail.html", context)


def book_update(request, id=None):
    instance = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "book_form.html", context)


def book_delete(request, id=None):
    instance = get_object_or_404(Book, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted: " + str(id))
    return redirect(book_list)


class BookList(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetail(APIView):
    def get(self, request, pk=None):
        res = Book.objects.get(id=pk)
        serializer = BookSerializer(res, many=False)
        return Response(serializer.data)


class BookSectionList(APIView):
    def get(self, request, pk=None):
        books = Book.objects.filter(section_id=pk)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)