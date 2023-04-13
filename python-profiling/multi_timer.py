from dataclasses import dataclass
from enum import Enum
from time import perf_counter_ns


@dataclass
class MTRecord:
    label: str
    time: int
    flags: int


class MTState(Enum):
    READY = "ready",
    RUNNING = "started",
    STOPPED = "stopped"


class MultiTimer:
    def __init__(self):
        self.records: list[MTRecord] = []
        self.state: MTState = MTState.READY

    def start(self):
        assert self.state is MTState.READY
        self.state = MTState.RUNNING
        self.record('[START]')

    def reset(self):
        assert self.state is MTState.STOPPED
        self.records = []
        self.state = MTState.READY

    def record(self, label: str, flags=0):
        assert self.state is MTState.RUNNING
        self.records.append(MTRecord(label, perf_counter_ns(), flags))

    @staticmethod
    def ns_to_sec(ns: int) -> float:
        return float(ns) / 1_000_000_000

    def report(self, prefix=""):
        assert self.state is MTState.RUNNING
        self.record("[STOP]")
        self.state = MTState.STOPPED

        prefix_width = len(prefix) + 1 if prefix else 0
        max_label_width = max([len(record.label) for record in self.records])
        record_count = len(self.records)
        total_time = self.records[-1].time - self.records[0].time

        header = "{label:{label_width}s} {prof_time:>15s}  {dur_ns:>15s}   {dur_s:>15s}  {per:>8s}".format(
            label="Label",
            label_width=max_label_width + prefix_width,
            prof_time="Time",
            dur_ns="Elapsed (ns)",
            dur_s="Elapsed (s)",
            per="% Time"
        )
        lines = ['---', header]

        for i in range(record_count):
            fields: list[str] = []
            if prefix:
                fields.append(prefix)

            fields.append(f"{self.records[i].label:{max_label_width}}")
            fields.append(f"{self.records[i].time:15d}")

            if i < record_count - 1:
                elapsed_time = self.records[i + 1].time - self.records[i].time
                fields.append(f"{elapsed_time:16d}")

                time_sec = self.ns_to_sec(elapsed_time)
                fields.append(f"{time_sec:17.9f}")

                percentage = elapsed_time / total_time * 100.0
                fields.append(f"{percentage:9.2f}")
            else:
                fields.append(f"[{total_time:15d}]")
                fields.append(f"[{self.ns_to_sec(total_time):15.9f}]")
                fields.append(f"{100.0:8.2f}")

            if self.records[i].flags > 0:
                fields.append(" " + "*" * self.records[i].flags)

            lines.append(" ".join(fields))

        print("\n".join(lines), flush=True)


if __name__ == '__main__':
    import random
    from time import sleep


    def run_one_test(multi_timer: MultiTimer):
        multi_timer.start()
        for label in ['alpha', 'beta', 'gamma']:
            nap_time = random.randint(0, 2)
            print(label, nap_time)
            sleep(nap_time)
            multi_timer.record(label, nap_time * 2)
        multi_timer.report()


    mt = MultiTimer()
    run_one_test(mt)
    mt.reset()
    run_one_test(mt)