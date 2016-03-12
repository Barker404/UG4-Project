
values = {}
for i in range(200, 1000, 200):
    filename = str(i) + "messages.csv"

    with open(filename, "r") as f:
        f.readline()
        for line in f.readlines():
            line = line.strip()
            parts = line.split(", ")
            prob = float(parts[3])
            percent = float(parts[0])
            if prob not in values:
                values[prob] = []
            values[prob].append(percent)

averages = {k: sum(v)/len(v) for (k, v) in values.items()}

with open("combined.csv", "w") as fw:
    fw.write("not closer prob, Average messages delivered (percent)\n")
    for (k, v) in sorted(averages.items()):
        fw.write("{}, {}\n".format(k, v))
