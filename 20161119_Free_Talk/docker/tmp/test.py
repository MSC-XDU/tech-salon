def g():
  for i in range(1,5):
    yield i**2

for i in g():
  print i