/*
 * P4A gear store configuration.
 *
 * This is the ONLY file you edit to switch the shop from demo to live.
 *
 * No keys live here, ever. This file ships to every visitor's browser, so it
 * holds nothing but a public URL. The Stripe secret key stays in the Apps
 * Script project's script properties, server side, where the public cannot
 * read it. See backend/google-apps-script/README.md.
 *
 * To go live:
 *   1. Deploy the Apps Script web app (backend/google-apps-script/GO-LIVE.md).
 *   2. Paste its web app URL into checkoutEndpoint below.
 *   3. Commit and push.
 *
 * Leave checkoutEndpoint empty to keep the store in safe demo mode: the
 * checkout button disables itself and explains why, so a half-finished setup
 * can never take someone's money without being able to fulfil it.
 */
window.P4A_GEAR = {
  /* Apps Script web app URL, e.g. https://script.google.com/macros/s/AKfy.../exec */
  checkoutEndpoint: '',

  /* Shown to the buyer if checkout is unavailable for any reason. */
  fallbackEmail: 'hello@p4a.xyz',

  currency: 'AUD'
};
