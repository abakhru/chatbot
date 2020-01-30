#!/usr/bin/env python

import socket


# List with multiple matches
class Format1:
    def __init__(self, data):
        self.too_broad = None
        if data[0].find("Aborting search") >= 0:
            self.too_broad = 1
        self.todo = list()
        for i in range(len(data)):
            try:
                t = data[i]
                tmp = t[t.index('(') + 1 : t.rindex(')')]
                self.todo.append(tmp)
            except ValueError as _:
                # If there isn't a paren set, we don't add it
                pass

    def __getitem__(self, which):
        return self.todo[which]

    def __len__(self):
        return len(self.todo)

    def get_todo_list(self):
        return self.todo

    def was_too_broad(self):
        return self.too_broad

    def __str__(self):
        return str(self.todo)


# Document describing a single net block
class Format2:
    def __init__(self, data):
        self.longname = data[0]
        ln = self.longname
        self.shortname = ln[0 : ln.index('(')].strip()
        self.netname = ln[ln.index('(') + 1 : ln.rindex(')')]
        self.addr = data[1].strip()
        csz = data[2].strip()
        self.city = csz[0 : csz.index(',')]
        rest = csz[csz.index(',') + 1 :]
        self.state, self.zip = rest.split()
        self.country = data[3].strip()

        self.fields = dict()
        for i in range(len(data)):
            a = data[i].split(': ', 2)
            if len(a) == 2:
                print("Split to", a)
                self.fields[a[0].strip()] = a[1].strip()
        print("Fields: ", self.fields)

    def get_address(self):
        return self.addr, self.city, self.state, self.zip

    def __str__(self):
        return f"A netblock named {self.netname} from {self.city}, {self.state}"


class Whois:
    def __init__(self, server='whois.arin.net'):
        self.server = server

    def lookup(self, spec):
        sock = None
        for res in socket.getaddrinfo(self.server, 43, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                sock = socket.socket(af, socktype, proto)
                sock.connect(sa)
            except OSError as msg:
                if sock:
                    sock.close()
                sock = None
                # Try the next address
                continue
            # If we got here, we have a socket
            break
        if not sock:
            raise OSError(msg)
        sendptr = 0
        str = spec + '\r\n'
        while sendptr < len(str):
            # sendptr = sendptr + sock.send(str[sendptr:])
            sendptr = sendptr + sock.send(str[sendptr:].encode())
        f = sock.makefile('r')
        rv = self.get_data(f)
        f.close()
        sock.close()
        return rv

    def get_data(self, f):
        data = self.read_file(f)
        if data[1][0:3] == '   ':
            rv = Format2(data)
        else:
            rv = Format1(data)
        return rv

    @staticmethod
    def read_file(f):
        rv = list()
        line = f.readline()
        while line != '':
            rv.append(line.rstrip())
            line = f.readline()
        return rv

    def get_ip_address(self, t):
        r = self.lookup(t)
        if isinstance(r, Format1):
            if r.was_too_broad():
                print("***")
                print("The search was too broad, results may not be accurate")
                print("***")
            rv = self.lookup(r[-1]).get_address()
        elif isinstance(r, Format2):
            rv = r.get_address()
        else:
            raise "Unknown result format." + r.__name__
        return rv


def main():
    w = Whois()
    # print(w.get_ip_address(argv[1]))
    # print(w.get_ip_address('google.com'))
    print(w.lookup('pepsi.com'))


if __name__ == '__main__':
    main()
