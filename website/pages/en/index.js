/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const CompLibrary = require('../../core/CompLibrary.js');
const MarkdownBlock = CompLibrary.MarkdownBlock; /* Used to read markdown */
const Container = CompLibrary.Container;
const GridBlock = CompLibrary.GridBlock;

const siteConfig = require(process.cwd() + '/siteConfig.js');

function imgUrl(img) {
  return siteConfig.baseUrl + 'img/' + img;
}

function docUrl(doc, language) {
  return siteConfig.baseUrl + 'docs/' + (language ? language + '/' : '') + doc;
}

function pageUrl(page, language) {
  return siteConfig.baseUrl + (language ? language + '/' : '') + page;
}

class Button extends React.Component {
  render() {
    return (
      <div className="pluginWrapper buttonWrapper">
        <a className="button" href={this.props.href} target={this.props.target}>
          {this.props.children}
        </a>
      </div>
    );
  }
}

Button.defaultProps = {
  target: '_self',
};

const SplashContainer = props => (
  <div className="homeContainer">
    <div className="homeSplashFade">
      <div className="wrapper homeWrapper">{props.children}</div>
    </div>
  </div>
);

const Logo = props => (
  <div className="projectLogo">
    <img src={props.img_src} />
  </div>
);

const ProjectTitle = props => (
  <h2 className="projectTitle">
    {siteConfig.title}
    <small>{siteConfig.tagline}</small>
  </h2>
);

const PromoSection = props => (
  <div className="section promoSection">
    <div className="promoRow">
      <div className="pluginRowBlock">{props.children}</div>
    </div>
  </div>
);

class HomeSplash extends React.Component {
  render() {
    let language = this.props.language || '';
    return (
      <SplashContainer>
        <Logo img_src={imgUrl('BMO.svg')} />
        <div className="inner">
          <ProjectTitle />
          <PromoSection>
            {/* <Button href="#try">Try It Out</Button> */}
            <Button href={docUrl('getting_started.html', language)}>Getting Started</Button>
            <Button href="https://moe.readthedocs.io/en/latest/index.html">API</Button>
            <Button href="http://cegal.gitlab.io/MOE/blog/">Blog</Button>
          </PromoSection>
        </div>
      </SplashContainer>
    );
  }
}

const Block = props => (
  <Container
    padding={['bottom', 'top']}
    id={props.id}
    background={props.background}>
    <GridBlock align="center" contents={props.children} layout={props.layout} />
  </Container>
);

const Features = props => (
  <Block layout="fourColumn">
    {[
      {
        content: '3 simple interface: Readers, Writers, and Mailers',
        image: imgUrl('modular.svg'),
        imageAlign: 'top',
        title: 'Modular',
      },
      {
        content: 'Use it as CLI app or connect your own hardware to it',
        image: imgUrl('diy.svg'),
        imageAlign: 'top',
        title: 'DIY',
      },
      {
        content: 'Its your network: you choose who has access to it and how to send the data',
        image: imgUrl('p2p.svg'),
        imageAlign: 'top',
        title: 'P2P',
      },
    ]}
  </Block>
);

const FeatureCallout = props => (
  <div
    className="productShowcaseSection paddingBottom"
    style={{textAlign: 'center'}}>
    <h2>Features</h2>
    {/* <MarkdownBlock>its Free and Open Source Software!</MarkdownBlock> */}
  </div>
);

const LearnHow = props => (
  <Block background="light">
    {[
      {
        content: '<br />Check our **[Getting Started](http://cegal.gitlab.io/MOE/docs/getting_started.html)** tutorial.<br /><br />\
        You just want to code your own components? check out our **[API](https://moe.readthedocs.io/en/latest/index.html)**<br /><br />\
        You just want to build a physical **MOE**? check out our **[Hardware Samples](http://cegal.gitlab.io/MOE/docs/getting_started.html#hardware)**',
        image: imgUrl('BMO_flat.jpg'),
        imageAlign: 'right',
        title: 'Learn How',
      },
    ]}
  </Block>
);

const Community = props => (
  <Block id="try">
    {[
      {
        content: '<br />Are you having issues with **MOE**? Open up an issue on our **[Issue Tracker](https://gitlab.com/cegal/MOE/issues)**<br /><br />\
        Do you want to contribute new ideas? Check our **[Contribution Guidelines](https://gitlab.com/cegal/MOE/blob/master/CONTRIBUTING.md)**<br /><br />\
        Don\'t know what you want? Just browse the Project\'s **[GitLab Repository](https://gitlab.com/cegal/MOE)**!',
        image: imgUrl('gitlab.svg'),
        imageAlign: 'left',
        title: 'Community',
      },
    ]}
  </Block>
);

const Description = props => (
  <Block background="dark">
    {[
      {
        content: '<br />Send encoded messages through the internet in any encoding you want. <br /><br /> \
        You can implement your own input, output, and transportation modules. <br /><br /> \
        This project is primarily a CLI application, but we also include documentation on how to build a physical **MOE** Raspberry Pi Device.',
        image: imgUrl('BMO.svg'),
        imageAlign: 'right',
        title: 'Description',
      },
    ]}
  </Block>
);

const ComponentsCallout = props => (
  <div
    className="productShowcaseSection paddingTop"
    style={{textAlign: 'center'}}>
    <h2>Components</h2>
    {/* <MarkdownBlock>its Free and Open Source Software!</MarkdownBlock> */}
  </div>
);

const Components = propr => (
  <Block layout="fourColumn">
    {[
      {
        content: 'Read a message from the user<br />\
        e.g. Camera, Button, Stdin',
        title: 'Reader',
      },
      {
        content: 'Output a received message<br />\
        e.g. Buzzer, Printer, Stdout',
        title: 'Writer',
      },
      {
        content: 'Encode/decode a message to any given dictionnary fed to it',
        title: 'Encoder',
      },
      {
        content: 'Send/receive a message over the Internet<br \>\
        e.g. Gmail, Twilio, API',
        title: 'Mailer',
      },
    ]}
  </Block>
);

const Showcase = props => {
  if ((siteConfig.users || []).length === 0) {
    return null;
  }
  const showcase = siteConfig.users
    .filter(user => {
      return user.pinned;
    })
    .map((user, i) => {
      return (
        <a href={user.infoLink} key={i}>
          <img src={user.image} alt={user.caption} title={user.caption} />
        </a>
      );
    });

  return (
    <div className="productShowcaseSection paddingBottom">
      <h2>{"Who's Using This?"}</h2>
      <p>This project is used by all these people</p>
      <div className="logos">{showcase}</div>
      <div className="more-users">
        <a className="button" href={pageUrl('users.html', props.language)}>
          More {siteConfig.title} Users
        </a>
      </div>
    </div>
  );
};

class Index extends React.Component {
  render() {
    let language = this.props.language || '';

    return (
      <div>
        <HomeSplash language={language} />
        <div className="mainContainer">
          <Features />
          <FeatureCallout />
          <LearnHow />
          <Community />
          <Description />
          <ComponentsCallout />
          <Components />
          <Showcase language={language} />
        </div>
      </div>
    );
  }
}

module.exports = Index;
