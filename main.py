from src.pipeline import resoluteProNouns
import sys


def main():
    # counter for the output
    right, candWasThere, rand, near, allResolutedProns, allRightProns = 0, 0, 0, 0, 0, 0

    # training-data: 1,16
    # test-data: 16,20
    # all-data: 1,20
    start, end = 16, 20

    print("Starting to analyze texts:")
    sys.stdout.write("\r{0}/{1}".format(0, end-start))

    # loop thorugh all texts and try to resolute pronouns
    for i in range(start, end):
        tester = resoluteProNouns(i)

        # increase all counter
        right += tester.right
        candWasThere += tester.candidateWasThereCount
        rand += tester.randomBase
        near += tester.nearestBase
        allResolutedProns += tester.allProns
        allRightProns += tester.allRightProns

        sys.stdout.write("\r{0}/{1}".format(i-start+1, end - start))
        sys.stdout.flush()

    # print results
    print(f"\nRun was successful.\n################")
    print(f"{allRightProns} Pronouns should have been resoluted.")
    print(f"{format((allResolutedProns/allRightProns)*100, '.2f')} % Pronouns were resoluted.")
    print(f"{format((candWasThere/allRightProns)*100, '.2f')} % Pronoun & Candidate found")
    print("##############")
    print(f"{format((right/ allRightProns)*100, '.2f')} % Sys-Precision")
    print(f"{format((right / allResolutedProns)*100, '.2f')} % Sys-Recall")
    print("#############")
    print(f"{format((near/ allRightProns)*100, '.2f')} % Near-Precision")
    print(f"{format((near / allResolutedProns)*100, '.2f')} % Near-Recall")
    print("##############")
    print(f"{format((right/ candWasThere)*100, '.2f')} % Sys-ESR")
    print(f"{format((near / candWasThere)*100, '.2f')} % Near-ESR")
    print(f"{format((rand / candWasThere)*100, '.2f')} % Rand-ESR")


main()
