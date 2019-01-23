
h_start, h_end = 7, 21
no_start, no_step = 4, 2
c_no_start, c_no_step = 5, None
no_prefix = 27
c_no_prefix = 13
origin = 'TAC'
start_mm = 50
end_h_offset = 1
end_mm = 50
dest = 'ZUY'

h_start = int(input('start hour'))
h_end = int(input('end hour'))
no_start = int(input('train no start'))
no_step = int(input('train no step'))
no_prefix = int(input('train no prefix'))
origin = input('origin station')
dest = input('destination station')
start_mm = int(input('start minute'))
end_mm = int(input('end minute'))
end_h_offset = int(input('end hour offset'))

no = no_start
c_no = c_no_start

for h in range(h_start, h_end):
    if c_no_start and c_no_step and c_no_prefix:
        print("{}{:02} {} {:02}:{:02} {} {:02}:{:02} {}{:02}".format(
            no_prefix, no, origin, h, start_mm, dest, h + end_h_offset, end_mm, 
            c_no_prefix, c_no))
        c_no += c_no_step
    else:
        print("{}{:02} {} {:02}:{:02} {} {:02}:{:02}".format(
            no_prefix, no, origin, h, start_mm, dest, h + end_h_offset, end_mm))

    no += no_step

