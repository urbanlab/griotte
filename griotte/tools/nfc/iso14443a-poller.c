/**
 * Based on libnfc's quick_start_example1.c
 */

// To compile :
// $ gcc -o quick_start_example1 quick_start_example1.c -lnfc

#include <stdlib.h>
#include <nfc/nfc.h>
#include <signal.h>
#include <stdlib.h>

nfc_device *pnd;
// Allocate only a pointer to nfc_context
nfc_context *context;

void sigint_handler(int) {
  // Close NFC device
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
    printf("%02x", pbtData[szPos]);
  }
  printf("\n");
}

static void
poll_tags()
{
// Poll for a ISO14443A (MIFARE) tag
  const nfc_modulation nmMifare = {
    .nmt = NMT_ISO14443A,
    .nbr = NBR_106,
  };

  nfc_target nt;

  do {
    if (nfc_initiator_select_passive_target(pnd, nmMifare, NULL, 0, &nt) > 0) {
      // printf("The following (NFC) ISO14443A tag was found:\n");
      // printf("    ATQA (SENS_RES): ");
      // print_hex(nt.nti.nai.abtAtqa, 2);
      // printf("       UID (NFCID%c): ", (nt.nti.nai.abtUid[0] == 0x08 ? '3' : '1'));
      print_hex(nt.nti.nai.abtUid, nt.nti.nai.szUidLen);
      return
      // printf("      SAK (SEL_RES): ");
      // print_hex(&nt.nti.nai.btSak, 1);
      // if (nt.nti.nai.szAtsLen) {
      //   printf("          ATS (ATR): ");
      //   print_hex(nt.nti.nai.abtAts, nt.nti.nai.szAtsLen);
      // }
    }
  } while (true);
}

int
main(int argc, const char *argv[])
{
  struct sigaction act;
  act.sa_handler = sigint_handler;
  sigaction(SIGINT, &act, NULL);

  // Initialize libnfc and set the nfc_context
  nfc_init(&context);
  if (context == NULL) {
    printf("Unable to init libnfc (malloc)\n");
    exit(EXIT_FAILURE);
  }

  // Display libnfc version
  const char *acLibnfcVersion = nfc_version();
  (void)argc;
  printf("%s uses libnfc %s\n", argv[0], acLibnfcVersion);

  // Open, using the first available NFC device which can be in order of selection:
  //   - default device specified using environment variable or
  //   - first specified device in libnfc.conf (/etc/nfc) or
  //   - first specified device in device-configuration directory (/etc/nfc/devices.d) or
  //   - first auto-detected (if feature is not disabled in libnfc.conf) device
  pnd = nfc_open(context, NULL);

  if (pnd == NULL) {
    printf("ERROR: %s\n", "Unable to open NFC device.");
    exit(EXIT_FAILURE);
  }
  // Set opened NFC device to initiator mode
  if (nfc_initiator_init(pnd) < 0) {
    nfc_perror(pnd, "nfc_initiator_init");
    exit(EXIT_FAILURE);
  }

  printf("NFC reader: %s opened\n", nfc_device_get_name(pnd));

  poll_tags();
}
