/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const CompLibrary = require('../../core/CompLibrary.js');
const Container = CompLibrary.Container;
const GridBlock = CompLibrary.GridBlock;

const siteConfig = require(process.cwd() + '/siteConfig.js');

function docUrl(doc, language) {
  return siteConfig.baseUrl + 'docs/' + (language ? language + '/' : '') + doc;
}

class Help extends React.Component {
  render() {
    let language = this.props.language || '';
    const supportLinks = [
      {
        content: `For a tutorial on how to use MOE, visit the **[Getting Started](http://cegal.gitlab.io/MOE/docs/getting_started.html)** walkthrough.<br />
        For the API interface and software architecture, visit MOE's **[API documentation](https://moe.readthedocs.io/en/latest/)**.<br />
        For updates on the project and other related stories, visit the **[Blog](http://cegal.gitlab.io/MOE/blog/)**.`,
        title: 'Browse Docs',
      },
      {
        content: "Find out what new features are planned and what known issues are currently being fixed in our **[Issue Tracker](https://github.com/CamiloGarciaLaRotta/MOE/issues)**",
        title: 'Stay up to date',
      },
    ];

    return (
      <div className="docMainWrapper wrapper">
        <Container className="mainContainer documentContainer postContainer">
          <div className="post">
            <header className="postHeader">
              <h2>Need help?</h2>
            </header>
            <p>This project is maintained with love, we are happy to help.</p>
            <GridBlock contents={supportLinks} layout="twoColumn" />
          </div>
        </Container>
      </div>
    );
  }
}

module.exports = Help;
