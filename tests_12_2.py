import unittest
import inspect


class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self, sampling_interval=1):
        self.distance += sampling_interval * self.speed * 2

    def walk(self, sampling_interval=1):
        self.distance += sampling_interval * self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self, sampling_interval=1):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run(sampling_interval)
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner('Усэйн', 10)
        self.andrey = Runner('Андрей', 9)
        self.nik = Runner('Ник', 3)

    @classmethod
    def tearDownClass(cls):
        print()
        for test in cls.all_results:
            print({k: str(v) for k, v in cls.all_results[test].items()})

    def test_first_tournament(self):
        tour = Tournament(90, self.usain, self.nik)
        results = tour.start()
        self.all_results[inspect.stack()[0][3]] = results
        self.assertTrue('Ник' == results[len(results)].name)

    def test_second_tournament(self):
        tour = Tournament(90, self.andrey, self.nik)
        results = tour.start()
        self.all_results[inspect.stack()[0][3]] = results
        self.assertTrue('Ник' == results[len(results)].name)

    def test_third_tournament(self):
        tour = Tournament(90, self.usain, self.andrey, self.nik)
        results = tour.start()
        self.all_results[inspect.stack()[0][3]] = results
        self.assertTrue('Ник' == results[len(results)].name)

    def test_third_tournament_additional(self):
        tour = Tournament(8, self.nik, self.andrey, self.usain)
        results = tour.start(0.1)
        self.all_results[inspect.stack()[0][3]] = results
        self.assertTrue('Ник' == results[len(results)].name)


if __name__ == '__main__':
    unittest.main()
