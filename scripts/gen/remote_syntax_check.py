# -*- coding: utf-8 -*-
import ast, sys, os
os.chdir('/data/xiaojingwen/carla_clear_acc')
for f in ['carla_synth_clear.py', 'batch_v2_clear.py']:
    ast.parse(open(f, encoding='utf-8').read())
    print(f, 'AST_OK', os.path.getsize(f))
