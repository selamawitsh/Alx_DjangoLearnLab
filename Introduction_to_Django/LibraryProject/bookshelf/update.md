book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
Book.objects.get(id=book.id)
# Output: <Book: Nineteen Eighty-Four by George Orwell>
