/**
 * Based on libnfc's quick_start_example1.c
 */

// To compile :
// $ gcc -o iso14443a-poller iso14443a-poller.c -lnfc

#include <stdlib.h>
#include <nfc/nfc.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

nfc_device *pnd;
// Allocate only a pointer to nfc_context
nfc_context *context;

void sigint_handler(int whatever) {
  fprintf(stderr, "SIGINT trapped");

  // Abort & close NFC device
  nfc_abort_command(pnd);
  nfc_close(pnd);

  // Release the context
  nfc_exit(context);
  exit(EXIT_SUCCESS);
}

static void
print_hex(const uint8_t *pbtData, const size_t szBytes)
{
  size_t  szPos;

  for (szPos = 0; szPos < szBytes; szPos++) {
    fprintf(stdout, "%02x", pbtData[szPos]);
  }
  fprintf(stdout, "\n");
  fflush(stdout);
}

static void
print_usage(const char *progname)
{
  fprintf(stderr, "usage: %s [-d x]\n", progname);
  fprintf(stderr, "  -d x\t wait x msecs after each tag detection\n");
}

static void
poll_tags(int delay)
{
// Poll for a ISO14443A (MIFARE) tag
  const nfc_modulation nmMifare = {
    .nmt = NMT_ISO14443A,
    .nbr = NBR_106,
  };

  nfc_target nt;

  do {
    if (nfc_initiator_select_passive_target(pnd, nmMifare, NULL, 0, &nt) > 0) {
      print_hex(nt.nti.nai.abtUid, nt.nti.nai.szUidLen);
      usleep(delay);
    }
  } while (true);
}

int
main(int argc, const char *argv[])
{
  int delay = 100;
  struct sigaction act;
  act.sa_handler = sigint_handler;
  sigaction(SIGINT, &act, NULL);

  if (argc != 1) {
    if ((argc == 3) && (0 == strcmp("-d", argv[1]))) {
      delay = atoi(argv[2]);
    } else {
      print_usage(argv[0]);
      exit(EXIT_FAILURE);
    }
  }

  // Initialize libnfc and set the nfc_context
  nfc_init(&context);
  if (context == NULL) {
    fprintf(stderr, "Unable to init libnfc (malloc)\n");
    exit(EXIT_FAILURE);
  }

  // Display libnfc version
  const char *acLibnfcVersion = nfc_version();
  fprintf(stderr, "%s uses libnfc %s\n", argv[0], acLibnfcVersion);

  // Open, using the first available NFC device which can be in order of selection:
  //   - default device specified using environment variable or
  //   - first specified device in libnfc.conf (/etc/nfc) or
  //   - first specified device in device-configuration directory (/etc/nfc/devices.d) or
  //   - first auto-detected (if feature is not disabled in libnfc.conf) device
  pnd = nfc_open(context, NULL);

  if (pnd == NULL) {
    fprintf(stderr, "ERROR: %s\n", "Unable to open NFC device.");
    exit(EXIT_FAILURE);
  }
  // Set opened NFC device to initiator mode
  if (nfc_initiator_init(pnd) < 0) {
    nfc_perror(pnd, "nfc_initiator_init");
    exit(EXIT_FAILURE);
  }

  fprintf(stderr, "NFC reader: %s opened\n", nfc_device_get_name(pnd));

  setbuf(stdout , NULL);
  poll_tags(delay*1000);
}
