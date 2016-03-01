Python Truth Table Constructor v 1.0

INSTALLATION
------------------------------------------------
Go to python.org, download Python 2.6.x and install.
Open terminal and install ply (Python Lex & Yacc)
python easy_install ply


USAGE
------------------------------------------------
Open terminal and run truthtable_constructor.py:
user@localhost:~> python truthtable_constructor.py

Now you can input logical expressions.

Example 1 (syllogism proof):
> ((p->q)&(q->r))->(p->r)
[0, 0, 1, 1, 0, 0, 1, 1]   q
[0, 0, 0, 0, 1, 1, 1, 1]   p
[0, 1, 0, 1, 0, 1, 0, 1]   r
[1, 1, 1, 1, 0, 0, 1, 1] (p -> q)
[1, 1, 0, 1, 1, 1, 0, 1] (q -> r)
[1, 1, 0, 1, 0, 0, 0, 1] ((p -> q) AND (q -> r))
[1, 1, 1, 1, 0, 1, 0, 1] (p -> r)
[1, 1, 1, 1, 1, 1, 1, 1] ((p -> q) AND (q -> r)) -> (p -> r)

Example 2:
> (p&(p->(r|s))&(r->q)&(s->q))->q
[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]   q
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]   p
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]   s
[0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]   r
[0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1] (r OR s)
[1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1] (p -> (r OR s))
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1] p AND (p -> (r OR s))
[1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1] (r -> q)
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1] p AND (p -> (r OR s)) AND (r -> q)
[1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1] (s -> q)
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1] (p AND (p -> (r OR s)) AND (r -> q) AND (s -> q))
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] (p AND (p -> (r OR s)) AND (r -> q) AND (s -> q)) -> q

If you want to just type 'exit' or 'quit':
> exit
