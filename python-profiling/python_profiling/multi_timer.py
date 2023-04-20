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
    def __init__(self) -> None:
        self.records: list[MTRecord] = []
        self.state: MTState = MTState.READY

    def start(self) -> None:
        assert self.state is MTState.READY
        self.state = MTState.RUNNING
        self.record('[START]')

    def reset(self) -> None:
        assert self.state is MTState.STOPPED
        self.records = []
        self.state = MTState.READY

    def record(self, label: str, flags=0) -> None:
        assert self.state is MTState.RUNNING
        self.records.append(MTRecord(label, perf_counter_ns(), flags))

    @staticmethod
    def ns_to_sec(ns: int) -> float:
        return float(ns) / 1_000_000_000

    def report(self, prefix="") -> str:
        assert self.state is MTState.RUNNING
        self.record("[STOP]")
        self.state = MTState.STOPPED

        prefix_width = len(prefix) + 1 if prefix else 0
        max_label_width = max([len(record.label) for record in self.records])
        record_count = len(self.records)
        total_time = self.records[-1].time - self.records[0].time

        header = "{label:{label_width}s} {prof_time:>15s}  {dur_s:>15s}  {per:>8s}".format(
            label="Label",
            label_width=max_label_width + prefix_width,
            prof_time="Time Stamp",
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

                time_sec = self.ns_to_sec(elapsed_time)
                fields.append(f"{time_sec:16.9f}")

                percentage = elapsed_time / total_time * 100.0
                fields.append(f"{percentage:9.2f}")
            else:
                fields.append(f"[{self.ns_to_sec(total_time):15.9f}]")
                fields.append(f"{100.0:8.2f}")

            if self.records[i].flags > 0:
                fields.append(" " + "*" * self.records[i].flags)

            lines.append(" ".join(fields))

        return "\n".join(lines)
