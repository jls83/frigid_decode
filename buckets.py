from itertools import chain

frigid = [[],
 [551, 552, 553, 554, 555],
 [576, 577, 578, 579, 580, 581, 582],
 [605],
 [624, 625, 626, 627, 628, 629, 630],
 [650, 651, 652, 653, 654, 655, 656],
 [1653, 1654, 1655, 1656, 1657],
 [1678, 1679, 1680, 1681, 1682, 1683],
 [4511, 4512, 4513, 4514, 4515, 4516],
 [8963, 8964, 8965, 8966, 8967, 8968],
 [8989],
 [8991, 8992],
 [8994],
 [19990],
 [20011, 20012, 20013, 20014, 20015, 20016],
 [40022, 40023, 40024, 40025],
 [40027],
 [40029]]

nums = [[],
 [551, 552, 553, 554, 555, 556],
 [576, 577, 578, 579, 580],
 [625, 626, 627, 628, 629, 630],
 [650, 651, 652, 653, 654, 655],
 [1653, 1654, 1655, 1656],
 [1678, 1679, 1680, 1681, 1682],
 [4512, 4513, 4514],
 [8965, 8966, 8967, 8968],
 [8990],
 [8992],
 [20011, 20012, 20013],
 [20015],
 [40021],
 [40023, 40024, 40025]]

vals = reduce(lambda a, c: a + c, chain(frigid, nums))


