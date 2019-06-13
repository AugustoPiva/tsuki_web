from escpos import helpers

for impl in helpers.find_implementations(sort_by='model.name'):
    print('{:.<25} {}'.format(impl.model.name, impl.fqname))
