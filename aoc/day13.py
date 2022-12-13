import operator
import functools


def parse_integer(s):
    count = 0
    while "0" <= s[count] <= "9":
        count += 1
    return int(s[:count]), s[count:]


def parse_list(s):
    packet = []
    s = s[1:]

    while s:
        if s[0] == "]":
            return packet, s[1:]

        if s[0] == ",":
            s = s[1:]
        elif s[0] == "[":
            item, s = parse_list(s)
            packet.append(item)
        else:
            item, s = parse_integer(s)
            packet.append(item)


def parse_packet(s):
    packet, s = parse_list(s)
    return packet


def compare_packets(ll, lr):
    for l, r in zip(ll, lr):
        if isinstance(l, int) and isinstance(r, int):
            diff = l - r
        elif isinstance(l, int):
            diff = compare_packets([l], r)
        elif isinstance(r, int):
            diff = compare_packets(l, [r])
        else:
            diff = compare_packets(l, r)

        if diff != 0:
            return diff

    return len(ll) - len(lr)


def run(data):
    packets = [parse_packet(line) for line in data.splitlines() if line]

    sum_indices = sum(
        1 + (i // 2)
        for i in range(0, len(packets) - 1, 2)
        if compare_packets(packets[i], packets[i + 1]) < 0
    )

    divider_packets = [[[2]], [[6]]]
    ordered_packets = sorted(
        packets + divider_packets, key=functools.cmp_to_key(compare_packets)
    )
    decoder_key = operator.mul(
        ordered_packets.index(divider_packets[0]) + 1,
        ordered_packets.index(divider_packets[1]) + 1,
    )

    return sum_indices, decoder_key
