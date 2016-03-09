#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import itertools
from crawler.scraper import Scraper
from crawler import parser
from crawler import race_parser
from crawler import storage


def read_paths(filename):
    with open(filename, 'r') as f:
        paths = [line.strip() for line in f.readlines()]
    return paths


def range_year_month(start_year, start_month, end_year, end_month):
    if start_year > end_year:
        raise Exception('start_year must be less than or equal end_year.')

    if start_year == end_year and start_month > end_month:
        raise Exception('start day must be less than or equal end day.')

    if start_year != end_year:
        front_date_list = [(start_year, month)
                           for month in range(start_month, 12 + 1)]
        behind_date_list = [(end_year, month)
                            for month in range(1, end_month + 1)]
        main_date_list = list(itertools.product(
            range(start_year + 1, end_year), range(1, 13)))
        date_list = front_date_list + main_date_list + behind_date_list
    else:
        date_list = [(start_year, month)
                     for month in range(start_month, end_month + 1)]

    return date_list


def parse_args():
    parser = argparse.ArgumentParser(
        description='This script is crawler in yahoo keiba.')
    parser.add_argument('--start_year', type=int, choices=range(2000, 2999),
                        default=2010)
    parser.add_argument('--start_month', type=int, choices=range(1, 13),
                        default=1)
    parser.add_argument('--end_year', type=int, choices=range(2000, 2999),
                        default=datetime.date.today().year)
    parser.add_argument('--end_month', type=int, choices=range(1, 13),
                        default=datetime.date.today().month)

    return parser.parse_args()


def main(date_list):

    # fetch race/list/ paths
    paths = ["schedule/list/{}/?month={}".format(year, month)
             for year, month in date_list]
    race_list_filename = 'path/race_list.txt'
    Scraper(parser.parse_schedule_list,
            storage.PathStorage(race_list_filename).store).crawl(paths)

    # fetch race/result/ paths
    paths = read_paths(race_list_filename)
    race_result_filename = 'path/race_result.txt'
    Scraper(parser.parse_race_list,
            storage.PathStorage(race_result_filename).store).crawl(paths)

    # get race info, race result, jockey path, horse path, trainer path
    paths = read_paths(race_result_filename)
    jockey_filename = 'path/jockey.txt'
    horse_filename = 'path/horse.txt'
    trainer_filename = 'path/trainer.txt'
    Scraper(race_parser.RaceResultParser().parse,
            storage.RaceResultStorage(
                jockey_filename,
                horse_filename,
                trainer_filename).store).crawl(paths)

#     paths = read_paths(jockey_filename)
#     Scraper(parser.parse_jockey,
#             storage.JockeyStorage().store).crawl(paths)
#     paths = read_paths(horse_filename)
#     Scraper(parser.parse_horse,
#             storage.HorseStorage().store).crawl(paths)
#     paths = read_paths(jockey_filename)
#     Scraper(parser.parse_trainer,
#             storage.TrainerStorage().store).crawl(paths)

if __name__ == "__main__":
    args = parse_args()

    date_list = range_year_month(args.start_year, args.start_month,
                                 args.end_year, args.end_month)

    main(date_list)
