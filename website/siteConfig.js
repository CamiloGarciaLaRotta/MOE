/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// See https://docusaurus.io/docs/site-config.html for all the possible
// site configuration options.

/* List of projects/orgs using your project for the users page */
// const users = [
//   {
//     caption: 'CraftChop',
//     // You will need to prepend the image path with your baseUrl
//     // if it is not '/', like: '/test-site/img/BMO.svg'.
//     image: '/img/craftchop.png',
//     infoLink: 'http://thecraftchop.com',
//     pinned: true,
//   },
//   {
//     caption: 'ReadTheDocs',
//     // You will need to prepend the image path with your baseUrl
//     // if it is not '/', like: '/test-site/img/BMO.svg'.
//     image: '/img/readthedocs.png',
//     infoLink: 'https://readthedocs.org/',
//     pinned: true,
//   },
// ];

const siteConfig = {
  title: 'The MOE Project' /* title for your website */,
  tagline: 'Morse Over Ethernet',
  url: 'https://cegal.gitlab.io' /* your website url */,
  baseUrl: '/MOE/' /* base url for your project */,
  // For github.io type URLs, you would set the url and baseUrl like:
  //   url: 'https://facebook.github.io',
  //   baseUrl: '/test-site/',

  // Used for publishing and more
  projectName: 'moe-site',
  organizationName: 'Camilo Garcia La Rotta',
  // For top-level user or org sites, the organization is still the same.
  // e.g., for the https://JoelMarcey.github.io site, it would be set like...
  //   organizationName: 'JoelMarcey'

  // For no header links in the top nav bar -> headerLinks: [],
  headerLinks: [
    { href: 'https://moe.readthedocs.io/en/latest/index.html', label: 'API' },
    { blog: true, label: 'Blog' },
    { doc: 'getting_started', label: 'Getting Started' },
    { href: 'https://github.com/CamiloGarciaLaRotta/MOE', label: 'GitHub' },
    { page: 'help', label: 'Help' },
  ],

  // If you have users set above, you add it here:
  // users,

  /* path to images for header/footer */
  headerIcon: 'img/BMO.svg',
  footerIcon: 'img/BMO.svg',
  favicon: 'img/favicon.png',

  /* colors for website */
  colors: {
    primaryColor: '#5ABEA6',
    secondaryColor: '#6BE0D0',
  },

  /* custom fonts for website */
  /*fonts: {
    myFont: [
      "Times New Roman",
      "Serif"
    ],
    myOtherFont: [
      "-apple-system",
      "system-ui"
    ]
  },*/

  // This copyright info is used in /core/Footer.js and blog rss/atom feeds.
  copyright:
    'Camilo Garcia La Rotta ' + new Date().getFullYear(),

  highlight: {
    // Highlight.js theme to use for syntax highlighting in code blocks
    theme: 'default',
  },

  // Add custom scripts here that would be placed in <script> tags
  // scripts: ['https://buttons.github.io/buttons.js'],

  /* On page navigation for the current documentation page */
  onPageNav: 'separate',

  /* Open Graph and Twitter card images */
  // ogImage: 'img/docusaurus.png',
  // twitterImage: 'img/docusaurus.png',

  // You may provide arbitrary config keys to be used as needed by your
  // template. For example, if you need your repo's URL...
  //   repoUrl: 'https://github.com/facebook/test-site',

  // blog related configuration
  blogSidebarCount: 'ALL',
};

module.exports = siteConfig;
